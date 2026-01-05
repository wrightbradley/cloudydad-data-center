{ pkgs, ... }:

{
  home.packages = with pkgs; [
    kubectl
    k9s
    helm
    kustomize
    fluxcd
  ];
}
