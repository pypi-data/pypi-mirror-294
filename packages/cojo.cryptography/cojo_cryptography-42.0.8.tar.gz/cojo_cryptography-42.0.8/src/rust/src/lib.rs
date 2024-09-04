// This file is dual licensed under the terms of the Apache License, Version
// 2.0, and the BSD License. See the LICENSE file in the root of this repository
// for complete details.

#![deny(rust_2018_idioms, clippy::undocumented_unsafe_blocks)]
#![allow(unknown_lints, non_local_definitions)]

use crate::error::CryptographyResult;
#[cfg(CRYPTOGRAPHY_OPENSSL_300_OR_GREATER)]
use openssl::provider;
use std::env;

mod asn1;
mod backend;
mod buf;
mod error;
mod exceptions;
pub(crate) mod oid;
mod padding;
mod pkcs7;
pub(crate) mod types;
mod x509;

#[cfg(CRYPTOGRAPHY_OPENSSL_300_OR_GREATER)]
#[pyo3::prelude::pyclass(frozen, module = "cryptography.hazmat.bindings._rust")]
struct LoadedProviders {
    legacy: Option<provider::Provider>,
    _default: provider::Provider,
}

#[pyo3::prelude::pyfunction]
fn openssl_version() -> i64 {
    openssl::version::number()
}

#[pyo3::prelude::pyfunction]
fn is_fips_enabled() -> bool {
    cryptography_openssl::fips::is_enabled()
}

#[cfg(CRYPTOGRAPHY_OPENSSL_300_OR_GREATER)]
fn _initialize_providers() -> CryptographyResult<LoadedProviders> {
    // As of OpenSSL 3.0.0 we must register a legacy cipher provider
    // to get RC2 (needed for junk asymmetric private key
    // serialization), RC4, Blowfish, IDEA, SEED, etc. These things
    // are ugly legacy, but we aren't going to get rid of them
    // any time soon.
    let load_legacy = env::var("CRYPTOGRAPHY_OPENSSL_NO_LEGACY")
        .map(|v| v.is_empty() || v == "0")
        .unwrap_or(true);
    let legacy = if load_legacy {
        let legacy_result = provider::Provider::load(None, "legacy");
        _legacy_provider_error(legacy_result.is_ok())?;
        Some(legacy_result?)
    } else {
        None
    };
    let _default = provider::Provider::load(None, "default")?;
    Ok(LoadedProviders { legacy, _default })
}

fn _legacy_provider_error(success: bool) -> pyo3::PyResult<()> {
    if !success {
        return Err(pyo3::exceptions::PyRuntimeError::new_err(
            "OpenSSL 3.0's legacy provider failed to load. This is a fatal error by default, but cryptography supports running without legacy algorithms by setting the environment variable CRYPTOGRAPHY_OPENSSL_NO_LEGACY. If you did not expect this error, you have likely made a mistake with your OpenSSL configuration."
        ));
    }
    Ok(())
}

#[pyo3::prelude::pymodule]
fn _rust(py: pyo3::Python<'_>, m: &pyo3::types::PyModule) -> pyo3::PyResult<()> {
    m.add_function(pyo3::wrap_pyfunction!(padding::check_pkcs7_padding, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(padding::check_ansix923_padding, m)?)?;
    m.add_class::<oid::ObjectIdentifier>()?;

    m.add_submodule(asn1::create_submodule(py)?)?;
    m.add_submodule(pkcs7::create_submodule(py)?)?;
    m.add_submodule(exceptions::create_submodule(py)?)?;

    let x509_mod = pyo3::prelude::PyModule::new(py, "x509")?;
    crate::x509::certificate::add_to_module(x509_mod)?;
    crate::x509::common::add_to_module(x509_mod)?;
    crate::x509::crl::add_to_module(x509_mod)?;
    crate::x509::csr::add_to_module(x509_mod)?;
    crate::x509::sct::add_to_module(x509_mod)?;
    crate::x509::verify::add_to_module(x509_mod)?;
    m.add_submodule(x509_mod)?;

    let ocsp_mod = pyo3::prelude::PyModule::new(py, "ocsp")?;
    crate::x509::ocsp_req::add_to_module(ocsp_mod)?;
    crate::x509::ocsp_resp::add_to_module(ocsp_mod)?;
    m.add_submodule(ocsp_mod)?;

    m.add_submodule(cryptography_cffi::create_module(py)?)?;

    let openssl_mod = pyo3::prelude::PyModule::new(py, "openssl")?;
    cfg_if::cfg_if! {
        if #[cfg(CRYPTOGRAPHY_OPENSSL_300_OR_GREATER)] {
            let providers = _initialize_providers()?;
            if providers.legacy.is_some() {
                openssl_mod.add("_legacy_provider_loaded", true)?;
            } else {
                openssl_mod.add("_legacy_provider_loaded", false)?;
            }
            openssl_mod.add("_providers", providers)?;
        } else {
            // default value for non-openssl 3+
            openssl_mod.add("_legacy_provider_loaded", false)?;
        }
    }
    openssl_mod.add_function(pyo3::wrap_pyfunction!(openssl_version, m)?)?;
    openssl_mod.add_function(pyo3::wrap_pyfunction!(error::raise_openssl_error, m)?)?;
    openssl_mod.add_function(pyo3::wrap_pyfunction!(error::capture_error_stack, m)?)?;
    openssl_mod.add_function(pyo3::wrap_pyfunction!(is_fips_enabled, m)?)?;
    openssl_mod.add_class::<error::OpenSSLError>()?;
    crate::backend::add_to_module(openssl_mod)?;
    m.add_submodule(openssl_mod)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::_legacy_provider_error;

    #[test]
    fn test_legacy_provider_error() {
        assert!(_legacy_provider_error(true).is_ok());
        assert!(_legacy_provider_error(false).is_err());
    }
}
