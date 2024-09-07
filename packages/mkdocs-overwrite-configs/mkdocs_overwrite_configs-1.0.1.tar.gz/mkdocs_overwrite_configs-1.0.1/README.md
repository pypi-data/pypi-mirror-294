A simple plugin that will override configs that previous plugins have messed.

I made this plugin for the sole reason that I need to use the same config for a standalone build and a backstage integration. For some reason, the backstage-techdocs-core plugin messes with the config and I need to override it to make it work.

## Usage

```yaml
theme:
  palette: &palette
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to system preference
plugins:
  - overwrite-configs:
      theme:
        palette: *palette
```
