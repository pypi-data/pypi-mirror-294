use pyo3::prelude::*;

// Functions to wrap
#[pyfunction]
fn exact_raw_extract(
    s: String, 
    pattern: String, 
    case_insensitive: bool, 
    special_char_insensitive: bool,
    strategies: Vec<String>
) -> PyResult<Vec<(usize, usize, f64)>> {
    Ok(search::exact_raw_extract::extract(s, pattern, case_insensitive, special_char_insensitive, strategies))
}

#[pyfunction]
fn exact_token_extract(
    s: String, 
    pattern: String, 
    tokenizer_pattern: String,
    case_insensitive: bool, 
    special_char_insensitive: bool
) -> PyResult<Vec<(usize, usize, f64)>> {
    Ok(search::exact_token_extract::extract(s, pattern, tokenizer_pattern, case_insensitive, special_char_insensitive))
}

#[pyfunction]
fn fuzzy_raw_extract(
    s: String, 
    pattern: String, 
    case_insensitive: bool, 
    special_char_insensitive: bool,
    metric: String,
    threshold: f64,
    threshold_kind: u8,
    strategies: Vec<String>
) -> PyResult<Vec<(usize, usize, f64)>> {
    Ok(search::fuzzy_raw_extract::extract(s, pattern, case_insensitive, special_char_insensitive, metric, threshold, threshold_kind, strategies))
}

#[pyfunction]
fn fuzzy_token_extract(
    s: String, 
    pattern: String, 
    tokenizer_pattern: String,
    case_insensitive: bool, 
    special_char_insensitive: bool,
    metric: String,
    threshold: f64,
    threshold_kind: u8,
    strategies: Vec<String>
) -> PyResult<Vec<(usize, usize, f64)>> {
    Ok(search::fuzzy_token_extract::extract(s, pattern, tokenizer_pattern, case_insensitive, special_char_insensitive, metric, threshold, threshold_kind, strategies))
}

/// A Python module implemented in Rust.
#[pymodule]
fn searchrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(exact_raw_extract, m)?)?;
    m.add_function(wrap_pyfunction!(exact_token_extract, m)?)?;
    m.add_function(wrap_pyfunction!(fuzzy_raw_extract, m)?)?;
    m.add_function(wrap_pyfunction!(fuzzy_token_extract, m)?)?;
    Ok(())
}
