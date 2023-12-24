local opt = vim.opt -- for conciseness

-- Numeracion de las lineas
opt.relativenumber = true
opt.number = true

-- tabs & indentation
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.autoindent = true

-- Line wrapping
opt.wrap = false

-- Search setting
opt.ignorecase = true
opt.smartcase = true

-- Cursor line
opt.cursorline = true

-- appearance
opt.termguicolors = true
opt.background = "dark"
opt.signcolumn = "yes"

-- Backspace
opt.backspace = "indent,eol,start"

-- Clipboard 
opt.clipboard:append("unnamedplus")

-- Splitt Windows
opt.splitright = true
opt.splitbelow = true

opt.iskeyword:append("-")

-- Remember last cursosr position
local group = vim.api.nvim_create_augroup("jump_last_position", { clear = true })
vim.api.nvim_create_autocmd(
	"BufReadPost",
	{callback = function()
			local row, col = unpack(vim.api.nvim_buf_get_mark(0, "\""))
			if {row, col} ~= {0, 0} then
				vim.api.nvim_win_set_cursor(0, {row, 0})
			end
		end,
	group = group
	}
)
