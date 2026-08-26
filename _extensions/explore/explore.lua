-- {{< explore "prompt text" >}}  or  {{< explore "prompt text" recency=true >}}
-- Renders the prompt visibly plus prefill links (ChatGPT, Claude, Perplexity) and a copy button.

local function urlencode(s)
  return (s:gsub("[^A-Za-z0-9%-%._~]", function(c)
    return string.format("%%%02X", string.byte(c))
  end))
end

local function htmlescape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local NUDGE = " Search the web for current information, and cite your sources with their dates."

return {
  ["explore"] = function(args, kwargs, meta)
    if not quarto.doc.isFormat("html") then
      return pandoc.Null()
    end
    local prompt = pandoc.utils.stringify(args[1] or "")
    local recency = pandoc.utils.stringify(kwargs["recency"] or "false") == "true"
    local sent = prompt
    if recency then sent = prompt .. NUDGE end
    local enc = urlencode(sent)
    local html = string.format([[
<div class="explore">
<span class="explore-label">Ask AI:</span><span class="explore-prompt">%s</span>
<div class="explore-buttons">
<a href="https://chatgpt.com/?q=%s" target="_blank" rel="noopener">ChatGPT</a>
<a href="https://claude.ai/new?q=%s" target="_blank" rel="noopener">Claude</a>
<a href="https://www.perplexity.ai/search?q=%s" target="_blank" rel="noopener">Perplexity</a>
<button type="button" data-prompt="%s" onclick="navigator.clipboard.writeText(this.dataset.prompt);this.textContent='Copied';setTimeout(()=>this.textContent='Copy prompt',1500)">Copy prompt</button>
</div>
</div>]], htmlescape(prompt), enc, enc, enc, htmlescape(sent))
    return pandoc.RawBlock("html", html)
  end
}
