{ config, pkgs, lib, ... }:

{
  home.stateVersion = "24.05";
  home.username = "developer";
  home.homeDirectory = "/home/developer";
  home.packages = with pkgs; [
    git
    lazygit
    gh
  ];
}
