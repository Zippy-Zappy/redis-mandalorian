document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("episodeForm");
    const list = document.getElementById("episodeList");
    const updateFormContainer = document.getElementById("updateForm");
    const updateForm = document.getElementById("updateEpisodeForm");
    const updateEpisodeId = document.getElementById("updateEpisodeId");
    const updateName = document.getElementById("updateName");
    const updateSeason = document.getElementById("updateSeason");
    const updatePrice = document.getElementById("updatePrice");

    const loadEpisodes = () => {
        fetch("/episodes")
            .then(res => res.json())
            .then(data => {
                list.innerHTML = "";
                data.forEach(ep => {
                    console.log(ep); // Para debug
                    //if (ep.status !== "Status.AVAILABLE") return;

                    const item = document.createElement("li");
                    const text = document.createTextNode(
                        `#${ep.number} - ${ep.name} (T${ep.season}) - $${ep.price} `
                    );
                    item.appendChild(text);

                    // Botón Borrar
                    const deleteBtn = document.createElement("button");
                    deleteBtn.textContent = "🗑️ Borrar";
                    deleteBtn.classList.add("delete-btn");
                    deleteBtn.addEventListener("click", () => {
                        const confirmDelete = confirm(`¿Borrar episodio #${ep.number}?`);
                        if (confirmDelete) {
                            fetch(`/delete/${ep.number}`, {
                                method: "DELETE"
                            })
                            .then(res => res.json())
                            .then(() => loadEpisodes());
                        }
                    });

                    // Botón Actualizar
                    const updateBtn = document.createElement("button");
                    updateBtn.textContent = "✏️ Actualizar";
                    updateBtn.classList.add("update-btn");
                    updateBtn.addEventListener("click", () => {
                        updateEpisodeId.value = ep.number;
                        updateName.value = ep.name;
                        updateSeason.value = ep.season;
                        updatePrice.value = ep.price;
                        updateFormContainer.style.display = "block";
                    });

                    // Botón Alquilar
                    const rentBtn = document.createElement("button");
                    rentBtn.textContent = "🎬 Alquilar";
                    rentBtn.classList.add("rent-btn");
                    
                    rentBtn.addEventListener("click", () => {
                        const confirmRent = confirm(`¿Querés alquilar el episodio #${ep.number}?`);
                        if (confirmRent) {
                            fetch(`/rent/${ep.number}`, {
                                method: "PUT"
                            })
                            .then(res => res.json())
                            .then(rentRes => {
                                alert(rentRes.message);
                                return fetch(`/verify/${ep.number}`, {
                                    method: "PUT"
                                });
                            })
                            .then(res => res.json())
                            .then(verifyRes => {
                                alert(verifyRes.message);
                                loadEpisodes();
                            })
                            .catch(err => {
                                console.error("Error al alquilar/verificar:", err);
                                alert("Ocurrió un error al procesar el alquiler.");
                            });
                        }
                    });

                    item.appendChild(deleteBtn);
                    item.appendChild(updateBtn);
                    item.appendChild(rentBtn);
                    list.appendChild(item);
                });
            });
    };

    // Formulario de agregar
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const payload = {
            number: document.getElementById("number").value,
            name: document.getElementById("name").value,
            season: document.getElementById("season").value,
            price: document.getElementById("price").value
        };

        fetch("/insert", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(() => {
            form.reset();
            loadEpisodes();
        });
    });

    // Formulario de actualizar
    updateForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const payload = {
            name: updateName.value.trim(),
            season: updateSeason.value.trim(),
            price: updatePrice.value.trim()
        };

        if (!payload.name || !payload.season || !payload.price) {
            alert("Por favor completá todos los campos.");
            return;
        }

        fetch(`/update/${updateEpisodeId.value}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            updateForm.reset(); // Esto ahora funciona porque apuntamos bien al form
            updateFormContainer.style.display = "none";
            loadEpisodes();
        })
        .catch(err => console.error("Error en actualización:", err));
    });

    loadEpisodes();
});
