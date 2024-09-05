{
  lib,
  makes_inputs,
  nixpkgs,
  python_pkgs,
  python_version,
}:
let
  make_bundle = commit: sha256:
    let
      raw_src = builtins.fetchTarball {
        inherit sha256;
        url =
          "https://gitlab.com/dmurciaatfluid/purity/-/archive/${commit}/purity-${commit}.tar";
      };
      src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
    in import "${raw_src}/build" {
      makesLib = makes_inputs;
      inherit nixpkgs python_version src;
    };
  bundle = make_bundle "bc2621cb8b330474edc2d36407fc5a7e0b0db09c"
    "1cjrjhbypby2s0q456dja3ji3b1f3rfijmbrymk13blxsxavq183";  # v2.0.0
in bundle.build_bundle (
  default: required_deps: builder:
  builder lib
  (required_deps (python_pkgs // { inherit (default.python_pkgs) types-simplejson; }))
)
