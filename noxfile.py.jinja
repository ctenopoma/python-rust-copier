import nox


@nox.session
def lint(session):
    session.run("uv", "run", "ruff", "check")
    session.run("uv", "run", "ruff", "format", "--check")
    session.run("uv", "run", "pyrefly")


@nox.session
def test(session):
    session.run("uv", "run", "pytest")
    session.run("cargo", "fmt", "--", "--check")
    session.run("cargo", "clippy", "--", "-D", "warnings")
    session.run("cargo", "test")


@nox.session
def build(session):
    session.run("uv", "build")


@nox.session
def docs(session):
    session.run("uv", "run", "sphinx-build", "-b", "html", "docs", "build/docs")
