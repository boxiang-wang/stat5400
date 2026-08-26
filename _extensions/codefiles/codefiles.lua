-- {{< codefiles s1p1 >}} : buttons linking to notes/code/s1p1.{R,py,Rmd,ipynb} in the course repo,
-- shown only for the files that exist. Repo from `codespace-repo` in _quarto.yml.
local function exists(p) local f = io.open(p, "r"); if f then f:close(); return true end; return false end
return {
  ["codefiles"] = function(args, kwargs, meta)
    if not quarto.doc.isFormat("html") then return pandoc.Null() end
    local name = pandoc.utils.stringify(args[1] or "")
    local repo = meta["codespace-repo"] and pandoc.utils.stringify(meta["codespace-repo"]) or ""
    local root = quarto.project.directory or "."
    local icons = { R = "fa-brands fa-r-project", py = "fa-brands fa-python",
                    Rmd = "fa-brands fa-markdown", ipynb = "fa-solid fa-book-open" }
    local labels = { R = "R", py = "Python", Rmd = "Rmd", ipynb = "ipynb" }
    local out = {}
    for _, ext in ipairs({"R", "py", "Rmd", "ipynb"}) do
      local rel = "notes/code/" .. name .. "." .. ext
      if exists(root .. "/" .. rel) then
        table.insert(out, string.format(
          '<a class="codefile" href="https://github.com/%s/blob/main/%s" target="_blank" rel="noopener"><i class="%s"></i> %s</a>',
          repo, rel, icons[ext], labels[ext]))
      end
    end
    return pandoc.RawInline("html", table.concat(out, " "))
  end
}
