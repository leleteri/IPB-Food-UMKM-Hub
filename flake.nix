{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    python = pkgs.python312;
  in {
    devShells.${system} = {
      backend = pkgs.mkShell {
        packages = [
          (python.withPackages (ps:
            with ps; [
              typing
              fastapi
              uvicorn
              pydantic
              sqlalchemy
              alembic
              asyncpg
              passlib
              python-jose
              python-multipart
              email-validator
            ]))
          pkgs.postgresql_16
        ];
      };
    };
  };
}
