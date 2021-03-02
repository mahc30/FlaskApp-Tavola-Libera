var splash, login, registro, reset, reset_part2, lista_restaurantes, restaurante, menu, reserva;
var btn_ingresar, btn_reset, btn_registro, btn_cont_reset, btn_confirm_login, btn_confirm_login_2, btn_confirm_login_3, btns_volver, btn_restaurante, btn_menu, btn_reserva, btn_add_platos;
var secciones;
window.onload = () => {
    crearReferencias();
    agregarEventos();
    setTimeout(() => { irA(login); }, 2000);
}
function crearReferencias() {
    splash = document.getElementById("splash");
    login = document.getElementById("login");
    registro = document.getElementById("registro");
    reset = document.getElementById("reset");
    reset_part2 = document.getElementById("reset_part2");
    lista_restaurantes = document.getElementById("lista_restaurantes");
    restaurante = document.getElementById("restaurante");
    menu = document.getElementById("menu");
    reserva = document.getElementById("reserva")

    // Botones
    btn_ingresar = document.getElementById("btn_ingresar");
    btn_confirm_login = document.getElementById("btn_confirm_login");
    btn_confirm_login_2 = document.getElementById("btn_confirm_login_2");
    btn_confirm_login_3 = document.getElementById("btn_confirm_login_3");
    btn_reset = document.getElementById("btn_reset");
    btn_registro = document.getElementById("btn_registro");
    btn_cont_reset = document.getElementById("btn_cont_reset");
    btn_restaurante = document.getElementById("btn_restaurante");
    btn_menu = document.getElementById("btn_menu");
    btn_reserva = document.getElementById("btn_reserva");
    btn_add_platos = document.getElementById("btn_add_platos")
    btns_volver = document.querySelectorAll(".volver");


    secciones = [splash, login, registro, reset, reset_part2, lista_restaurantes, restaurante, menu, reserva];
}
function agregarEventos() {
    btn_ingresar.addEventListener("click", () => { irA(lista_restaurantes); });
    btn_reset.addEventListener("click", () => { irA(reset); });
    btn_registro.addEventListener("click", () => { irA(registro); });
    btn_confirm_login.addEventListener("click", () => { irA(login); });
    btn_confirm_login_2.addEventListener("click", () => { irA(login); });
    btn_confirm_login_3.addEventListener("click", () => { irA(login); });
    btn_cont_reset.addEventListener("click", () => { irA(reset_part2); });
    btn_restaurante.addEventListener("click", () => { irA(restaurante); });
    btn_menu.addEventListener("click", () => { irA(menu); });
    btn_reserva.addEventListener("click", () => { irA(reserva); });
    btn_add_platos.addEventListener("click", () => { irA(menu); });
    for (var i = 0; i < 20; i++) {
        btns_volver[i].addEventListener("click", () => { irA(login); });
    }
}
function ocultarSecciones() {
    for (i in secciones) {
        secciones[i].classList.add("ocultar");
    }
}
function irA(seccion) {
    ocultarSecciones();
    seccion.classList.remove("ocultar");
}