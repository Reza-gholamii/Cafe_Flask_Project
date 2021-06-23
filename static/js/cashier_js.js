function hamburger_open(){
    const menu = document.getElementById("nav_menu")
    const close = document.getElementById("hamburger_close")
    const open = document.getElementById("hamburger_open")
    const hero= document.getElementById("menu-position")
    open.style.display = "none"
    close.style.visibility = "visible"
    hero.appendChild(menu)
    hero.style.display = "inline-block"
    menu.style.display = "inline-block"

}

function hamburger_close(){
    const navparent = document.getElementById("nav_parent")
    const hero=  document.getElementById("nav_menu")
    const menu = document.getElementById("menu-position")
    const close = document.getElementById("hamburger_close")
    const open = document.getElementById("hamburger_open")
    open.style.removeProperty("display")
    close.style.visibility = "hidden"
    menu.style.display = "none"
    navparent.appendChild(hero)

}



