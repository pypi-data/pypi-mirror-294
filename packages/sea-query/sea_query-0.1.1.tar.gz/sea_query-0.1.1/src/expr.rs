use pyo3::prelude::*;
use sea_query::{
    expr::{Expr as SeaExpr, SimpleExpr as SeaSimpleExpr},
    query::{
        CaseStatement as SeaCaseStatement, Condition as SeaCondition, OnConflict as SeaOnConflict,
    },
    Alias, IntoCondition,
};

use crate::query::SelectStatement;
use crate::types::PyValue;

#[pyclass]
#[derive(Clone)]
pub struct SimpleExpr(pub SeaSimpleExpr);

#[pymethods]
impl SimpleExpr {
    fn __or__(&self, other: &Self) -> Self {
        Self(self.0.clone().or(other.0.clone()))
    }

    fn __and__(&self, other: &Self) -> Self {
        Self(self.0.clone().and(other.0.clone()))
    }

    fn __invert__(&self) -> Self {
        Self(self.0.clone().not())
    }
}

#[pyclass]
#[derive(Clone)]
pub struct Expr(pub SeaExpr);

#[pymethods]
impl Expr {
    #[staticmethod]
    #[pyo3(signature = (name, table=None))]
    fn column(name: String, table: Option<String>) -> Self {
        if let Some(table) = table {
            return Self(SeaExpr::col((Alias::new(table), Alias::new(name))));
        }
        Self(SeaExpr::col(Alias::new(name)))
    }

    #[staticmethod]
    fn value(value: PyValue) -> Self {
        Self(SeaExpr::val(&value))
    }

    #[allow(clippy::self_named_constructors)]
    #[staticmethod]
    fn expr(expr: Expr) -> Self {
        Self(SeaExpr::expr(expr.0.clone()))
    }

    #[pyo3(signature = (column, table=None))]
    fn equals(&self, column: String, table: Option<String>) -> SimpleExpr {
        if let Some(table) = table {
            return SimpleExpr(
                self.0
                    .clone()
                    .equals((Alias::new(table), Alias::new(column))),
            );
        }
        SimpleExpr(self.0.clone().equals(Alias::new(column)))
    }

    #[pyo3(signature = (column, table=None))]
    fn not_equals(&self, column: String, table: Option<String>) -> SimpleExpr {
        if let Some(table) = table {
            return SimpleExpr(
                self.0
                    .clone()
                    .equals((Alias::new(table), Alias::new(column))),
            );
        }
        SimpleExpr(self.0.clone().equals(Alias::new(column)))
    }

    fn eq(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().eq(&value))
    }

    fn ne(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().ne(&value))
    }

    fn gt(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().gt(&value))
    }

    fn gte(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().gte(&value))
    }

    fn lt(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().lt(&value))
    }

    fn lte(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().lte(&value))
    }

    fn is_(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().is(&value))
    }

    fn is_not(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_not(&value))
    }

    fn is_in(&self, values: Vec<PyValue>) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_in(&values))
    }

    fn is_not_in(&self, values: Vec<PyValue>) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_not_in(&values))
    }

    fn between(&self, start: PyValue, end: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().between(&start, &end))
    }

    fn not_between(&self, start: PyValue, end: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().not_between(&start, &end))
    }

    fn like(&self, value: String) -> SimpleExpr {
        SimpleExpr(self.0.clone().like(&value))
    }

    fn not_like(&self, value: String) -> SimpleExpr {
        SimpleExpr(self.0.clone().not_like(&value))
    }

    fn is_null(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_null())
    }

    fn is_not_null(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().is_not_null())
    }

    fn max(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().max())
    }

    fn min(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().min())
    }

    fn sum(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().sum())
    }

    fn count(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().count())
    }

    fn count_distinct(&self) -> SimpleExpr {
        SimpleExpr(self.0.clone().count_distinct())
    }

    fn if_null(&self, value: PyValue) -> SimpleExpr {
        SimpleExpr(self.0.clone().if_null(&value))
    }

    #[staticmethod]
    fn exists(query: SelectStatement) -> SimpleExpr {
        SimpleExpr(SeaExpr::exists(query.0))
    }

    #[staticmethod]
    fn case() -> CaseStatement {
        CaseStatement::new()
    }
}

#[pyclass]
#[derive(Clone)]
pub struct Condition(pub SeaCondition);

#[pymethods]
impl Condition {
    #[staticmethod]
    fn all() -> Self {
        Self(SeaCondition::all())
    }

    #[staticmethod]
    fn any() -> Self {
        Self(SeaCondition::any())
    }

    fn add(&self, expr: ConditionExpression) -> Self {
        Self(self.0.clone().add(expr.into_condition()))
    }

    fn __invert__(&self) -> Self {
        Self(self.0.clone().not())
    }
}

#[derive(FromPyObject)]
pub enum ConditionExpression {
    Condition(Condition),
    SimpleExpr(SimpleExpr),
}

impl IntoCondition for ConditionExpression {
    fn into_condition(self) -> SeaCondition {
        match self {
            ConditionExpression::Condition(cond) => cond.0,
            ConditionExpression::SimpleExpr(expr) => expr.0.into_condition(),
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct OnConflict(pub SeaOnConflict);

#[pymethods]
impl OnConflict {
    #[staticmethod]
    fn column(name: String) -> Self {
        Self(SeaOnConflict::column(Alias::new(name)))
    }

    #[staticmethod]
    fn columns(columns: Vec<String>) -> Self {
        Self(SeaOnConflict::columns(
            columns.iter().map(Alias::new).collect::<Vec<Alias>>(),
        ))
    }

    fn do_nothing(mut slf: PyRefMut<Self>) -> PyRefMut<Self> {
        slf.0.do_nothing();
        slf
    }

    // TODO: Implement missing methods
}

#[pyclass]
#[derive(Clone)]
pub struct CaseStatement(pub(crate) SeaCaseStatement);

#[pymethods]
impl CaseStatement {
    #[staticmethod]
    fn new() -> Self {
        Self(SeaCaseStatement::new())
    }

    fn when(&self, condition: ConditionExpression, then: Expr) -> Self {
        Self(self.0.clone().case(condition.into_condition(), then.0))
    }

    fn else_(&self, expr: Expr) -> Self {
        Self(self.0.clone().finally(expr.0))
    }
}

// PyO3 doesn't support generic types in methods, so we have to take a different approach
#[derive(FromPyObject)]
pub(crate) enum IntoSimpleExpr {
    SimpleExpr(SimpleExpr),
    Expr(Expr),
    CaseStatement(CaseStatement),
}

impl From<IntoSimpleExpr> for SeaSimpleExpr {
    fn from(expr: IntoSimpleExpr) -> Self {
        match expr {
            IntoSimpleExpr::SimpleExpr(expr) => expr.0,
            IntoSimpleExpr::Expr(expr) => expr.0.into(),
            IntoSimpleExpr::CaseStatement(case) => case.0.into(),
        }
    }
}
