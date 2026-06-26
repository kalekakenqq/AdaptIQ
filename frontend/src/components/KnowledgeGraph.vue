<script>
// демо-данные графа знаний по математическому анализу
export const DEFAULT_NODES = [
  { id: "limits", label: "Пределы", knowledge: 0.88, importance: 5 },
  { id: "derivatives", label: "Производные", knowledge: 0.81, importance: 5 },
  { id: "indefinite_integral", label: "Неопределённый интеграл", knowledge: 0.62, importance: 4 },
  { id: "definite_integral", label: "Определённый интеграл", knowledge: 0.55, importance: 4 },
  { id: "integrals", label: "Интегралы", knowledge: 0.49, importance: 5 },
  { id: "taylor_series", label: "Ряды Тейлора", knowledge: 0.34, importance: 4 },
  { id: "numeric_series", label: "Числовые ряды", knowledge: 0.41, importance: 3 },
  { id: "diff_equations", label: "Дифференциальные уравнения", knowledge: 0.22, importance: 5 },
  { id: "multivar_functions", label: "Функции нескольких переменных", knowledge: 0.28, importance: 4 },
  { id: "extrema", label: "Экстремумы", knowledge: 0.67, importance: 3 },
  { id: "lagrange_theorem", label: "Теорема Лагранжа", knowledge: 0.45, importance: 2 },
  { id: "newton_leibniz", label: "Формула Ньютона-Лейбница", knowledge: 0.58, importance: 3 },
];

export const DEFAULT_EDGES = [
  { source: "limits", target: "derivatives" },
  { source: "derivatives", target: "extrema" },
  { source: "derivatives", target: "lagrange_theorem" },
  { source: "derivatives", target: "indefinite_integral" },
  { source: "indefinite_integral", target: "definite_integral" },
  { source: "definite_integral", target: "integrals" },
  { source: "definite_integral", target: "newton_leibniz" },
  { source: "integrals", target: "diff_equations" },
  { source: "derivatives", target: "taylor_series" },
  { source: "taylor_series", target: "numeric_series" },
  { source: "derivatives", target: "multivar_functions" },
  { source: "multivar_functions", target: "extrema" },
];
</script>

<script setup>
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";

const props = defineProps({
  nodes: { type: Array, default: () => DEFAULT_NODES },
  edges: { type: Array, default: () => DEFAULT_EDGES },
});

const svgRef = ref(null);
const tooltip = ref({ visible: false, x: 0, y: 0, label: "", knowledge: 0 });

function knowledgeColor(knowledge) {
  if (knowledge > 0.7) return "#22c55e";
  if (knowledge >= 0.3) return "#eab308";
  return "#ef4444";
}

function render() {
  const width = 600;
  const height = 420;

  const svg = d3.select(svgRef.value);
  svg.selectAll("*").remove();

  const nodes = props.nodes.map((node) => ({ ...node }));
  const edges = props.edges.map((edge) => ({ ...edge }));

  const nodeRadius = (d) => 6 + d.importance * 1.5;

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3.forceLink(edges).id((d) => d.id).distance(80),
    )
    .force("charge", d3.forceManyBody().strength(-200))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("x", d3.forceX(width / 2).strength(0.1))
    .force("y", d3.forceY(height / 2).strength(0.1))
    .force("collide", d3.forceCollide().radius((d) => nodeRadius(d) + 14));

  const link = svg
    .append("g")
    .selectAll("line")
    .data(edges)
    .join("line")
    .attr("stroke", "#334155")
    .attr("stroke-width", 1.5);

  const node = svg
    .append("g")
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 0)
    .attr("fill", (d) => knowledgeColor(d.knowledge))
    .attr("stroke", "#0f172a")
    .attr("stroke-width", 2)
    .style("cursor", "pointer")
    .call(
      d3
        .drag()
        .on("start", (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }),
    );

  node
    .on("mouseover", (event, d) => {
      tooltip.value = {
        visible: true,
        x: event.offsetX,
        y: event.offsetY,
        label: d.label,
        knowledge: Math.round(d.knowledge * 100),
      };
    })
    .on("mousemove", (event) => {
      tooltip.value.x = event.offsetX;
      tooltip.value.y = event.offsetY;
    })
    .on("mouseout", () => {
      tooltip.value.visible = false;
    });

  // плавная анимация появления узлов
  node
    .transition()
    .duration(700)
    .delay((d, i) => i * 40)
    .attr("r", nodeRadius);

  const labels = svg
    .append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.label)
    .attr("font-size", "11px")
    .attr("fill", "#cbd5e1")
    .attr("text-anchor", "middle")
    .attr("dy", -16)
    .style("pointer-events", "none")
    .style("opacity", 0);

  labels.transition().duration(700).delay(400).style("opacity", 1);

  // удерживаем узлы в границах контейнера
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

  simulation.on("tick", () => {
    nodes.forEach((d) => {
      const r = nodeRadius(d) + 2;
      d.x = clamp(d.x, r, width - r);
      d.y = clamp(d.y, r + 14, height - r);
    });

    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    labels.attr("x", (d) => d.x).attr("y", (d) => d.y);
  });
}

onMounted(render);
watch(() => [props.nodes, props.edges], render, { deep: true });
</script>

<template>
  <div class="card relative overflow-hidden p-2">
    <svg ref="svgRef" viewBox="0 0 600 420" class="w-full rounded-lg bg-bg"></svg>
    <div
      v-if="tooltip.visible"
      class="pointer-events-none absolute z-10 rounded-lg bg-card px-3 py-2 text-xs shadow-lg ring-1 ring-white/10"
      :style="{ left: `${tooltip.x + 12}px`, top: `${tooltip.y + 12}px` }"
    >
      <p class="font-medium text-text">{{ tooltip.label }}</p>
      <p class="text-text/60">Знание: {{ tooltip.knowledge }}%</p>
    </div>
  </div>
</template>
