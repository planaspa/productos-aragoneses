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

const PROVINCIAS = ["Zaragoza", "Huesca", "Teruel"];

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
  provinciaStats: document.getElementById("provincia-stats"),
};

function provinciaFromLocation(location) {
  const parts = location.split(",").map((part) => part.trim());
  return parts.length > 1 ? parts[parts.length - 1] : location;
}

function provinciaClass(name) {
  return name.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
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

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderCard(record) {
  const prov = provinciaFromLocation(record.ubicacion_sede);
  const provCls = provinciaClass(prov);
  const municipio = record.ubicacion_sede.split(",")[0].trim();

  return `
    <article class="card ${provCls}" id="producto-${record.id}">
      <div class="card-header">
        <h2><a href="${escapeHtml(record.web)}" target="_blank" rel="noopener noreferrer">${escapeHtml(record.nombre)}</a></h2>
        <span class="${badgeClass(record.estado)}">${badgeLabel(record.estado)}</span>
      </div>
      <p class="meta">
        <span class="meta-company">${escapeHtml(record.nombre_compania)}</span>
        <span class="prov-tag ${provCls}">${escapeHtml(municipio)} · ${escapeHtml(prov)}</span>
      </p>
      <p class="card-desc">${escapeHtml(record.descripcion)}</p>
      <div class="card-footer">
        <span class="card-meta-id">id: <code>${escapeHtml(record.id)}</code></span>
        <a class="card-cta" href="${escapeHtml(record.web)}" target="_blank" rel="noopener noreferrer">
          Visitar →
        </a>
      </div>
    </article>
  `;
}

function countByProvincia(records) {
  const counts = Object.fromEntries(PROVINCIAS.map((p) => [p, 0]));
  for (const record of records) {
    const prov = provinciaFromLocation(record.ubicacion_sede);
    if (prov in counts) counts[prov] += 1;
  }
  return counts;
}

function renderProvinciaStats(records) {
  const counts = countByProvincia(records);
  els.provinciaStats.innerHTML = PROVINCIAS.map((prov) => {
    const n = counts[prov];
    if (!n) return "";
    return `<span class="prov-chip ${provinciaClass(prov)}">${prov}: ${n}</span>`;
  }).join("");
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
    els.results.innerHTML =
      `<p class="empty">Ningún producto coincide con los filtros. Prueba otra provincia o búsqueda.</p>`;
  } else {
    els.results.innerHTML = state.filtered.map(renderCard).join("");
  }

  const total = state.records.length;
  const shown = state.filtered.length;
  els.stats.innerHTML = `<strong>${shown}</strong> de ${total} · ${DATASETS[state.dataset].label}`;
  renderProvinciaStats(state.filtered);
}

function populateProvincias(records) {
  const provincias = [
    ...new Set(records.map((record) => provinciaFromLocation(record.ubicacion_sede))),
  ].sort((a, b) => a.localeCompare(b, "es"));

  els.provincia.innerHTML =
    `<option value="">Todas (Aragón)</option>` +
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
