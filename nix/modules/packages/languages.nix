{ pkgs, ... }:

{
  home.packages = with pkgs; [
    go
    nodejs_22
    pnpm
    python312
    uv
    rustc
    cargo
  ];
}
