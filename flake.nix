{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-21.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  nixConfig = {
    extra-binary-caches = [
      "https://cache.nixos.org/"
      "s3://l9o-nix-cache?endpoint=s3.us-east-1.wasabisys.com"
      "https://luizribeiro.cachix.org/"
    ];
    trusted-public-keys = [
      "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
      "nix-private-cache-1:i0M8QzO+0YA0N3sJn3MOIre6XqfXU5fFR55XWzgtqis="
      "luizribeiro.cachix.org-1:cptgSXacPnEoLyDCiPTBM7+3Af/YhQFqTpp2AVR508w="
    ];
  };

  outputs =
    { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachSystem [
      "aarch64-linux"
      "x86_64-darwin"
      "x86_64-linux"
    ]
      (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            python39
            python39Packages.poetry
            yarn
          ];
        };
      });
}
