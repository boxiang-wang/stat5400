-- {{< codespace-pill >}}            : the "▶ Run in Codespace" mode pill, clickable (opens the course Codespace)
-- {{< codespace "notes/run/x.R" >}} : small "file: notes/run/x.R" note under a block
-- {{< codespace >}}                 : plain "Open in Codespace" button (title row)
-- Repo comes from `codespace-repo` in _quarto.yml.
local function htmlescape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end
local function repo_url(meta)
  local repo = meta["codespace-repo"] and pandoc.utils.stringify(meta["codespace-repo"]) or ""
  return "https://codespaces.new/" .. repo .. "?quickstart=1"
end
return {
  ["codespace"] = function(args, kwargs, meta)
    if not quarto.doc.isFormat("html") then return pandoc.Null() end
    local file = pandoc.utils.stringify(args[1] or "")
    if file == "" then
      return pandoc.RawInline("html", string.format(
        '<a class="btn btn-sm btn-outline-dark" href="%s" target="_blank" rel="noopener"><i class="fa-solid fa-code"></i> Open in Codespace</a>',
        htmlescape(repo_url(meta))))
    end
    return pandoc.RawBlock("html", string.format(
      '<div class="codespace"><span class="codespace-file">file: <code>%s</code></span></div>', htmlescape(file)))
  end,
  ["codespace-pill"] = function(args, kwargs, meta)
    if not quarto.doc.isFormat("html") then return pandoc.Str("Run in Codespace") end
    return pandoc.RawInline("html", string.format(
      '<a class="mode mode-link" href="%s" target="_blank" rel="noopener"><i class="fa-solid fa-play"></i> Run in Codespace</a>',
      htmlescape(repo_url(meta))))
  end
}
