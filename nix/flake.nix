{
  description = "Cloudydad Nix Development Environment - Fish + nvim + TMUX";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager.url = "github:nix-community/home-manager/release-24.05";
  };

  outputs = { self, nixpkgs, home-manager }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
{
      homeConfigurations.developer = home-manager.lib.homeManagerConfiguration {
        inherit pkgs;
        modules = [
          ./modules/fish
          ./modules/nvim
          ./modules/tmux
          ./modules/starship
          ./modules/git
          ./modules/packages
        ];
      };
    };
}
