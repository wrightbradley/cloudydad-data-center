{ config, pkgs, lib, ... }:

{
  home.packages = with pkgs; [
    neovim
    nodejs_22
    pnpm
    python312
    lua
    go
    ripgrep
    fd
    xclip
    wl-clipboard
  ];

  home.activation.clone-nvim-config = lib.hm.dag.entryAfter ["linkGeneration"] ''
    NVIM_DIR="$HOME/.config/nvim"
    NVIM_REPO="https://github.com/wrightbradley/nvim.git"

    if [ ! -d "$NVIM_DIR" ]; then
      echo "Cloning nvim config from $NVIM_REPO to $NVIM_DIR"
      ${pkgs.git}/bin/git clone --depth 1 "$NVIM_REPO" "$NVIM_DIR"
    elif [ -z "$(ls -A $NVIM_DIR 2>/dev/null)" ]; then
      echo "nvim directory exists but is empty, recloning..."
      rm -rf "$NVIM_DIR"
      ${pkgs.git}/bin/git clone --depth 1 "$NVIM_REPO" "$NVIM_DIR"
    else
      echo "nvim config already exists at $NVIM_DIR"
    fi
  '';
}
