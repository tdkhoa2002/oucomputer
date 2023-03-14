function addToCart(id, name, price, image) {
    event.preventDefault()
    fetch('/api/cart', {
        method: 'post',
        body: JSON.stringify ({
            'id': id,
            'name': name,
            'price': price,
            'image': image,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementByClassName("cart-counter")
        for(let i=0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    })
    window.location.href = "/cart";
}


function deleteCart(product_id) {
    if (confirm("Bạn có muốn xóa sản phẩm này trong giỏ hàng không?") == true) {
        fetch(`/api/cart/${product_id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            console.info(data)
            let cart_counter = document.getElementsByClassName("cart-counter")
//            console.log(cart_counter)
            for (let i = 0; i < cart_counter.length; i++)
                cart_counter[i].innerText = data.total_quantity

            let cart_amount = document.getElementsByClassName("cart-amount")
//            console.log(cart_amount)
            for (let i = 0; i < cart_amount.length; i++)
                cart_amount[i].innerText = data.total_amount.toLocaleString("en-US")

            let cart_id = document.getElementById(`cart${product_id}`)
            cart_id.style.display = "none"
        }).catch(err => console.info(err)) // js promise
    }
}

function updateCart(product_id, object) {
    fetch(`/api/cart/${product_id}`, {
        method: "PUT",
        body: JSON.stringify({
            "quantity": object.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let cart_counter = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < cart_counter.length; i++)
            cart_counter[i].innerText = data.total_quantity

        let cart_amount = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < cart_amount.length; i++)
            cart_amount[i].innerText = data.total_amount.toLocaleString("en-US")
    }) // js promise
}

function pay() {
    if (confirm("Bạn có muốn thanh toán không ?") == true) {
        fetch("/api/pay").then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert("Có lỗi xày ra!")
        })
    }
}