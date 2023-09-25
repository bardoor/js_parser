for (let i = 1; i <= 5; i++) {
    if (temperature > 30) {
        return too_hot;
    } else if (temperature >= 20 && temperature <= 30) {
        return good;
    } else {
        return too_cold;
    }
}
