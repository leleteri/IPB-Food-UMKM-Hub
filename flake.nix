{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
  };
  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    python = pkgs.python312;

    # 1. Extract your package lists into standard Nix lists
    frontendPackages = [
      pkgs.nodejs_20
      pkgs.nodePackages.typescript
      pkgs.nodePackages.eslint
      pkgs.nodePackages.prettier
    ];

    backendPackages = [
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
          bcrypt
        ]))
      pkgs.postgresql_16
    ];
  in {
    devShells.${system} = {
      frontend = pkgs.mkShell {
        packages = frontendPackages;
      };

      backend = pkgs.mkShell {
        packages = backendPackages;
      };

      # 2. Combine the lists using the standard Nix list concatenation operator (++)
      #    and ensure 'packages' is spelled correctly.
      default = pkgs.mkShell {
        packages = frontendPackages ++ backendPackages;
      };
    };
  };
}
