document.addEventListener("DOMContentLoaded", function () {

        var btn = document.querySelectorAll("button");
        divC = document.querySelector("#chart_1");
        divF = document.querySelector("#chart_2");

        btn[0].addEventListener("click", function () {
            if (divC.style.display === "block"){
                divF.style.display = "none";
                // divF.style.display = "block";
            }
            else {
                divC.style.display = "none";
                divF.style.display = "block";
            }
        });

        btn[1].addEventListener("click", function () {
            if (divF.style.display === "none"){
                divF.style.display = "block";
                divC.style.display = "none";
                // divF.style.display = "block";
            }
            else {
                divF.style.display = "none";
                divC.style.display = "block";
            }
        });

});