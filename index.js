const API_URL = "http://127.0.0.1:8000";

document.getElementById("btnRekomendasi").onclick = async () => {

    const query = document.getElementById("query").value;
    const genre = document.getElementById("genre").value;
    const mood = document.getElementById("mood").value;

    const result = document.getElementById("result");
    const popular = document.getElementById("popular");

    const res = await fetch(`${API_URL}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, genre, mood })
    });

    const data = await res.json();

    // POPULAR
    popular.innerHTML = "";
    data.popular.forEach(j => {
        popular.innerHTML += `
        <div class="book">
            <div class="book-icon">🔥</div>
            <div class="book-content">
                <div class="book-title" title="${j}">
                    ${j}
                </div>
            </div>
        </div>`;
    });

    // RESULT
    result.innerHTML = "";
    data.recommendations.forEach(b => {
        const fullMeta = `${b.pengarang}  · ${b.klasifikasi}`;
        result.innerHTML += `
        <div class="book">
            <div class="book-icon">📘</div>
            <div class="book-content">
                <div class="book-title" title="${b.judul}">
                    ${b.judul}
                </div>
                <div class="Pengarang : " title="${fullMeta}">
                    ${fullMeta}
                   
                </div>
            </div>
        </div>`;
    });
};
