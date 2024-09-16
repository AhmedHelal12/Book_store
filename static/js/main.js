async function update_cart(e) {
    const { data } = await axios(e.dataset.url)
    const { message, items_count } = data
    console.log(items_count)
    console.log(message)

    // notify.success({
    //     message,
    //     dismissble: true,
    //     icon: false
    // })

    document.getElementById('cart-items-count').innerHTML = items_count
}

async function remove_cart(e) {
    await axios(e.dataset.url)
    location.reload()
}