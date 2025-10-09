{
  lib,
  python3Packages,
}:
python3Packages.buildPythonApplication {
  name = "area-backend";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  build-system = [python3Packages.hatchling];

  dependencies = with python3Packages; [
    aiosqlite
    bcrypt
    email-validator
    fastapi
    httpx
    pyjwt
    passlib
    sqlalchemy
    sqlmodel
    uvicorn
  ];

  optional-dependencies = with python3Packages; {
    dev = [
      fastapi-cli
      black
      isort
    ];
    testing = [
      pytest
      pytest-env
      pytest-cov
      pytest-xdist
      pytest-asyncio
    ];
  };

  nativeCheckInputs = with python3Packages; [
    pytestCheckHook
    pytest-env
    pytest-cov-stub
  ];

  meta = {
    description = "Modular workflow runner with FastAPI, SQLAlchemy, and MariaDB";
    license = lib.licenses.bsd3;
    maintainers = with lib.maintainers; [sigmanificient];
    mainProgram = "area";
  };
}
