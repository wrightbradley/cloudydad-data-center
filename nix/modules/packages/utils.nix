{ pkgs, ... }:

{
  home.packages = with pkgs; [
    fzf
    ripgrep
    eza
    bat
    fd
    tree
    htop
  ];
}
