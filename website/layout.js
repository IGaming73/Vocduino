window.onload = function() {
    var path = window.location.pathname;  // chemin du fichier actuel
    var filename = path.split("/").pop();  // nom du fichier
    var isIndex = filename == "index.html";  // donne true si le fichier est index, false sinon

    var header = `
        <h1 class="title"> Projet de reconnaissance vocale Vocduino </h1>
        <nav class="menu">
            <ul>
                <a href="${isIndex ? 'index.html' : '../index.html'}"><li> Accueil </li></a>
                <a href="${isIndex ? 'pages' : '.'}/info.html"><li> Informations </li></a>
                <a href="${isIndex ? 'pages' : '.'}/download.html"><li> Télécharger </li></a>
                <a href="${isIndex ? 'pages' : '.'}/doc.html"><li> Documentation </li></a>
                <a href="${isIndex ? 'pages' : '.'}/contact.html"><li> Contact </li></a>
            </ul>
        </nav>
    `;  // modèle du header

    var footer = `
        <p align="center">
        <br>      Nos réseaux :
        </p>
        <nav class="social" align="center">
            <ul>
                <a href="https://www.youtube.com/@ITech73" target="_blank">
                    <li>
                        <img src="${isIndex ? '.' : '..'}/imgs/youtube.png" width="25">
                        YouTube
                    </li>
                </a>
            </ul>
        </nav>
    `;  // modèle du footer

    // on remplace le header et le footer
    document.querySelector('header').innerHTML = header;
    document.querySelector('footer').innerHTML = footer;
};
