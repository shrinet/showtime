export function Authentication(goTo) {
    const isUserLoggedin = localStorage.getItem("token") || false
    !isUserLoggedin ? goTo('/login') : goTo(true)
}
