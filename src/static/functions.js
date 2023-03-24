function showPlaylists() {
    var formElement = document.getElementById("myFormPlaylists");
    var data = new FormData(formElement);
    fetch("/main-transfer", {
          method: "POST",
          body: data,
        })
        .then(resp => resp.text())
        .then(data => {
          document.getElementById("responseArea").innerHTML = data;
        })
        .catch(error => {
          console.error(error);
        });
}


