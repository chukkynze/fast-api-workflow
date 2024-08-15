# AcademyStack Aliases
# Format: alias shortName="your custom command here"

# Files
alias lh="ls -lah"

# Laravel Vapor
alias vpr="vendor/bin/vapor"
alias vapor="vendor/bin/vapor"

# GIT
alias gs="git status"
alias gb="git branch"

# Composer
alias cp-da="composer dump-autoload"

# Laravel
alias lvrts="(cd /var/www/html && php artisan route:list)"
alias lvmgsd="(cd /var/www/html && php artisan migrate:refresh --seed)"
alias lvdbsd="(cd /var/www/html && php artisan db:seed)"
alias lvmkmg="(cd /var/www/html && php artisan make:migration)"
alias lvmkctl="(cd /var/www/html && php artisan make:controller)"
alias lvmkmdl="(cd /var/www/html && php artisan make:model)"
alias lvmklwr="(cd /var/www/html && php artisan make:livewire)"