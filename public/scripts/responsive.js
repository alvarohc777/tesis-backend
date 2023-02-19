const sidebar = document.getElementById("sidebar")
let sidebarState = sidebar.dataset.state
console.log(sidebarState)
function toogleNav() {
    if (sidebarState === "closed") {
        sidebar.style.width = "250px";
        document.getElementById("openbtn").innerHTML = "x";
        document.getElementById("mainContent").style.marginLeft = "250px";
        document.getElementById('footer').style.marginLeft = '250px';

        sidebarState = "open"
    } else {
        sidebar.style.width = "0";
        document.getElementById("openbtn").innerHTML = "&#9002;&#9002;&#9002;";
        document.getElementById("mainContent").style.marginLeft = "0px";
        document.getElementById('footer').style.marginLeft = "0";
        sidebarState = "closed"
    }
}



sidebar.style.width = "250px";
document.getElementById("mainContent").style.marginLeft = "250px";
document.getElementById("footer").style.marginLeft = "250px";





