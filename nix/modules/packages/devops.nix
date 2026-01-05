{ pkgs, ... }:

{
  home.packages = with pkgs; [
    terraform
    tflint
    tfsec
    ansible
    ansible-lint
    jq
    yq
  ];
}
