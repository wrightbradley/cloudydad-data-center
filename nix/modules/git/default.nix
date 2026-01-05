{ config, pkgs, ... }:

{
  programs.git = {
    enable = true;
    userName = "Bradley Wright";
    userEmail = "bradley@cloudydad.world";
  };
}
