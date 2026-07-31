const DATASETS = {
  listado: {
    label: "Productos digitales",
    path: "datos/listado.json",
    nameField: "nombre",
  },
  ecommerce: {
    label: "E-commerce",
    path: "datos/ecommerce.json",
    nameField: "nombre",
  },
};

const state = {
  dataset: "listado",
  records: [],
  filtered: [],
};

const els = {
  tabs: document.querySelectorAll(".tab"),
  search: document.getElementById("search"),
  provincia: document.getElementById("provincia"),
  estado: document.getElementById("estado"),
  results: document.getElementById("results"),
  stats: document.getElementById("stats"),
};

function provinciaFromLocation(location) {
  const parts = location.split(",").map((part) => part.trim());
  return parts.length > 1 ? parts[parts.length - 1] : location;
}

function badgeClass(estado) {
  if (estado === "inactivo") return "badge inactivo";
  if (estado === "en_revision") return "badge en_revision";
  return "badge";
}

function badgeLabel(estado) {
  return (
    {
      activo: "Activo",
      inactivo: "Inactivo",
      en_revision: "En revisión",
    }[estado] || estado
  );
}

function renderCard(record) {
  const title = record.nombre;
  const web = record.web;
  return `
    <article class="card" id="producto-${record.id}">
      <div class="card-header">
        <h2><a href="${web}" target="_blank" rel="noopener noreferrer">${title}</a></h2>
        <span class="${badgeClass(record.estado)}">${badgeLabel(record.estado)}</span>
      </div>
      <p class="meta"><strong>${record.nombre_compania}</strong> · ${record.ubicacion_sede}</p>
      <p>${record.descripcion}</p>
      <div class="card-footer">
        <span>id: <code>${record.id}</code></span>
        <span>Verificado: ${record.ultima_verificacion}</span>
        <a href="${record.fuente}" target="_blank" rel="noopener noreferrer">Fuente</a>
      </div>
    </article>
  `;
}

function applyFilters() {
  const query = els.search.value.trim().toLowerCase();
  const provincia = els.provincia.value;
  const estado = els.estado.value;

  state.filtered = state.records.filter((record) => {
    const haystack = [
      record.nombre,
      record.nombre_compania,
      record.ubicacion_sede,
      record.descripcion,
      record.id,
    ]
      .join(" ")
      .toLowerCase();

    const matchesQuery = !query || haystack.includes(query);
    const matchesProvincia =
      !provincia || provinciaFromLocation(record.ubicacion_sede) === provincia;
    const matchesEstado = !estado || record.estado === estado;

    return matchesQuery && matchesProvincia && matchesEstado;
  });

  renderResults();
}

function renderResults() {
  if (!state.filtered.length) {
    els.results.innerHTML = `<p class="empty">No hay resultados con los filtros actuales.</p>`;
  } else {
    els.results.innerHTML = state.filtered.map(renderCard).join("");
  }

  const total = state.records.length;
  const shown = state.filtered.length;
  els.stats.textContent = `${shown} de ${total} registros · ${DATASETS[state.dataset].label}`;
}

function populateProvincias(records) {
  const provincias = [
    ...new Set(records.map((record) => provinciaFromLocation(record.ubicacion_sede))),
  ].sort((a, b) => a.localeCompare(b, "es"));

  els.provincia.innerHTML =
    `<option value="">Todas</option>` +
    provincias.map((p) => `<option value="${p}">${p}</option>`).join("");
}

async function loadDataset(name) {
  const config = DATASETS[name];
  const response = await fetch(config.path);
  if (!response.ok) {
    throw new Error(`No se pudo cargar ${config.path}`);
  }
  const payload = await response.json();
  state.dataset = name;
  state.records = payload.registros || [];
  populateProvincias(state.records);
  applyFilters();
}

function activateTab(name) {
  els.tabs.forEach((tab) => {
    const active = tab.dataset.dataset === name;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", active ? "true" : "false");
  });
}

function hashToState() {
  const hash = window.location.hash.replace(/^#\/?/, "");
  const match = hash.match(/^producto\/([a-z0-9-]+)$/);
  if (match) {
    els.search.value = match[1];
  }
}

els.tabs.forEach((tab) => {
  tab.addEventListener("click", async () => {
    const name = tab.dataset.dataset;
    activateTab(name);
    els.search.value = "";
    await loadDataset(name);
  });
});

els.search.addEventListener("input", applyFilters);
els.provincia.addEventListener("change", applyFilters);
els.estado.addEventListener("change", applyFilters);

window.addEventListener("hashchange", hashToState);

(async function init() {
  hashToState();
  try {
    await loadDataset("listado");
  } catch (error) {
    els.results.innerHTML = `<p class="empty">${error.message}</p>`;
  }
})();
