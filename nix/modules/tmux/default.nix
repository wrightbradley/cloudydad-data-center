{ config, pkgs, ... }:

{
  programs.tmux = {
    enable = true;
    terminal = "tmux-256color";
    historyLimit = 100000;

    plugins = with pkgs.tmuxPlugins; [
      tmux-sensible
      { plugin = tmux-resurrect; extraConfig = ''
        set -g @resurrect-capture-pane-contents 'on'
        set -g @resurrect-dir "$HOME/.config/tmux/resurrect"
        set -g @resurrect-strategy-nvim 'session'
        set -g @resurrect-restore 'on'
        set -g @resurrect-save 'S'
      '';}
      { plugin = tmux-continuum; extraConfig = ''
        set -g @continuum-restore 'on'
        set -g @continuum-boot 'on'
        set -g @continuum-save-interval '15'
      '';}
      tmux-fzf-url
      tmux-nerd-font-window-name
    ];

    extraConfig = ''
      set -g status-left-length 100
      set -g status-right-length 100
      set -g mode-keys vi
      set -g mouse on
      set -g default-terminal "screen-256color"
    '';
  };
}
