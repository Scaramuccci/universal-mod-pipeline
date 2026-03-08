local mod = {}
mod.name    = "sample_mod"
mod.version = "1.0.0"

function mod.on_load()
    print("[sample_mod] Loaded successfully.")
end

mod.on_load()
return mod
```

---

**`examples/sample_mod/assets/placeholder.txt`**
```
Replace this directory with real mod assets (textures, sounds, models, etc.)