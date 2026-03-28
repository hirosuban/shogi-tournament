const GEOJSON_PATH = "./data/shutoken.geojson";

const state = {
    selectedPrefectures: new Set(),
    mapLayersByPrefecture: new Map(),
};

const refs = {
    fromDate: document.getElementById("from-date"),
    toDate: document.getElementById("to-date"),
    resetButton: document.getElementById("reset-filters"),
    selectedPrefectures: document.getElementById("selected-prefectures"),
    loading: document.getElementById("loading"),
    error: document.getElementById("error"),
    resultCount: document.getElementById("result-count"),
    tournamentList: document.getElementById("tournament-list"),
};

const map = L.map("map", {
    zoomControl: true,
    scrollWheelZoom: false,
}).setView([35.75, 139.8], 8);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 12,
    minZoom: 7,
    attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

function regionStyle(isSelected = false) {
    return {
        color: "#1d2a3a",
        weight: 1.5,
        fillColor: isSelected ? "#c24f2b" : "#f2d7b3",
        fillOpacity: isSelected ? 0.85 : 0.68,
    };
}

function setLoading(isLoading) {
    refs.loading.hidden = !isLoading;
}

function setError(message = "") {
    refs.error.textContent = message;
    refs.error.hidden = !message;
}

function updateSelectedPrefectureText() {
    const names = Array.from(state.selectedPrefectures);
    refs.selectedPrefectures.textContent = names.length
        ? names.join(" / ")
        : "未選択（全件表示）";
}

function buildQueryParams() {
    const params = new URLSearchParams();

    for (const prefecture of state.selectedPrefectures) {
        params.append("prefecture", prefecture);
    }

    if (refs.fromDate.value) {
        params.append("from", refs.fromDate.value);
    }

    if (refs.toDate.value) {
        params.append("to", refs.toDate.value);
    }

    return params;
}

function renderEmpty() {
    refs.tournamentList.innerHTML = '<li class="empty">条件に一致する大会がありません。</li>';
    refs.resultCount.textContent = "0件";
}

function createTextElement(tagName, text, className = "") {
    const element = document.createElement(tagName);
    element.textContent = text;
    if (className) {
        element.className = className;
    }
    return element;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    if (Number.isNaN(date.getTime())) {
        return dateString;
    }
    return new Intl.DateTimeFormat("ja-JP", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        weekday: "short",
    }).format(date);
}

function renderTournaments(tournaments) {
    if (!tournaments.length) {
        renderEmpty();
        return;
    }

    refs.resultCount.textContent = `${tournaments.length}件`;
    refs.tournamentList.innerHTML = "";

    for (const item of tournaments) {
        const card = document.createElement("li");
        card.className = "card";

        card.appendChild(createTextElement("h3", item.name));

        const meta = document.createElement("div");
        meta.className = "meta";
        meta.appendChild(createTextElement("span", formatDate(item.date)));
        meta.appendChild(createTextElement("span", `${item.prefecture} / ${item.venue}`));
        card.appendChild(meta);

        const badges = document.createElement("div");
        badges.className = "badges";
        for (const token of (item.category || "").split(",").map((text) => text.trim())) {
            if (!token) {
                continue;
            }
            badges.appendChild(createTextElement("span", token, "badge"));
        }
        card.appendChild(badges);

        refs.tournamentList.appendChild(card);
    }
}

async function fetchAndRenderTournaments() {
    setLoading(true);
    setError("");

    try {
        const params = buildQueryParams();
        const url = `/tournaments${params.toString() ? `?${params}` : ""}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`大会データの取得に失敗しました: ${response.status}`);
        }

        const tournaments = await response.json();
        renderTournaments(tournaments);
    } catch (error) {
        refs.resultCount.textContent = "0件";
        refs.tournamentList.innerHTML = "";
        setError(error instanceof Error ? error.message : "不明なエラーが発生しました");
    } finally {
        setLoading(false);
    }
}

function syncMapStyles() {
    for (const [prefecture, layer] of state.mapLayersByPrefecture.entries()) {
        layer.setStyle(regionStyle(state.selectedPrefectures.has(prefecture)));
    }
}

function onPrefectureClick(prefecture) {
    if (state.selectedPrefectures.has(prefecture)) {
        state.selectedPrefectures.delete(prefecture);
    } else {
        state.selectedPrefectures.add(prefecture);
    }
    syncMapStyles();
    updateSelectedPrefectureText();
    fetchAndRenderTournaments();
}

async function loadGeoJson() {
    const response = await fetch(GEOJSON_PATH);
    if (!response.ok) {
        throw new Error(`GeoJSONの読み込みに失敗しました: ${response.status}`);
    }

    const geojson = await response.json();
    const layer = L.geoJSON(geojson, {
        style: () => regionStyle(false),
        onEachFeature: (feature, regionLayer) => {
            const prefecture = feature?.properties?.name;
            if (!prefecture) {
                return;
            }

            state.mapLayersByPrefecture.set(prefecture, regionLayer);
            regionLayer.bindTooltip(prefecture, { sticky: true });
            regionLayer.on("click", () => onPrefectureClick(prefecture));
            regionLayer.on("mouseover", () => {
                regionLayer.setStyle({ weight: 2.2 });
            });
            regionLayer.on("mouseout", () => {
                regionLayer.setStyle({ weight: 1.5 });
            });
        },
    }).addTo(map);

    map.fitBounds(layer.getBounds(), { padding: [12, 12] });
}

function resetFilters() {
    refs.fromDate.value = "";
    refs.toDate.value = "";
    state.selectedPrefectures.clear();
    syncMapStyles();
    updateSelectedPrefectureText();
    fetchAndRenderTournaments();
}

function attachEvents() {
    refs.fromDate.addEventListener("change", fetchAndRenderTournaments);
    refs.toDate.addEventListener("change", fetchAndRenderTournaments);
    refs.resetButton.addEventListener("click", resetFilters);
}

async function init() {
    attachEvents();
    updateSelectedPrefectureText();

    try {
        await loadGeoJson();
    } catch (error) {
        setError(error instanceof Error ? error.message : "地図の初期化に失敗しました");
    }

    fetchAndRenderTournaments();
}

void init();
