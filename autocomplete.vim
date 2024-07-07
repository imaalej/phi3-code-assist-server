function! SendToFlaskServer()
    " Save the current file
    write
    echo expand('%:p:h')
    " Get the content of the current file
    let l:content = join(getline(1, '$'), "\n")

    " Execute the Python script and capture the output
    let l:command = 'python3 send.py')
    let l:output = system(l:command, l:content)

    " Insert the result into the Vim buffer
    if v:shell_error
        echo "Error: " . l:output
    else
        call setline(1, split(l:output, "\n"))
    endif
endfunction

nnoremap <C-n> :call SendToFlaskServer()<CR>
