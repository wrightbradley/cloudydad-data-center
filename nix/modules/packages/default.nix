{ config, pkgs, lib, ... }:

{
  home.packages = lib.mkMerge [
    (import ./core.nix { inherit pkgs; }).home.packages
    (import ./languages.nix { inherit pkgs; }).home.packages
    (import ./kubernetes.nix { inherit pkgs; }).home.packages
    (import ./devops.nix { inherit pkgs; }).home.packages
    (import ./utils.nix { inherit pkgs; }).home.packages
  ];
}
