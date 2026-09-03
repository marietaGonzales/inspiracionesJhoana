let cart = {};

function addProduct(name, price) {
    if (!cart[name]) {
        cart[name] = {qty: 0, price: price};
    }
    cart[name].qty += 1;
    updateTable();
}

function updateTable() {
    let table = document.getElementById("table");
    table.innerHTML = "<tr><th>Product</th><th>Quantity</th><th>Subtotal</th></tr>";
    let total = 0;
    let detail = [];
    for (let [name, data] of Object.entries(cart)) {
        let subtotal = data.qty * data.price;
        total += subtotal;
        table.innerHTML += `<tr><td>${name}</td><td>${data.qty}</td><td>${subtotal}</td></tr>`;
        detail.push(`${name}:${data.qty}`);
    }
    document.getElementById("total").innerText = total;
    document.getElementById("detail").value = detail.join(",");
    document.getElementById("totalFinal").value = total;
}

function saveImage() {
    html2canvas(document.body).then(canvas => {
        var link = document.createElement('a');
        link.download = 'order.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}
