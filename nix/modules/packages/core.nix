{ pkgs, ... }:

{
  home.packages = with pkgs; [
    tmux
    fish
    starship
  ];
}
