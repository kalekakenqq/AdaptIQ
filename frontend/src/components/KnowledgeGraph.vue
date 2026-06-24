<script setup>
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";

const props = defineProps({
  nodes: {
    type: Array,
    default: () => [],
  },
  links: {
    type: Array,
    default: () => [],
  },
});

const svgRef = ref(null);

function render() {
  const svg = d3.select(svgRef.value);
  svg.selectAll("*").remove();

  const width = 600;
  const height = 400;

  const simulation = d3
    .forceSimulation(props.nodes)
    .force("link", d3.forceLink(props.links).id((d) => d.id).distance(80))
    .force("charge", d3.forceManyBody().strength(-150))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg
    .append("g")
    .selectAll("line")
    .data(props.links)
    .join("line")
    .attr("stroke", "#334155")
    .attr("stroke-width", 1.5);

  const node = svg
    .append("g")
    .selectAll("circle")
    .data(props.nodes)
    .join("circle")
    .attr("r", 9)
    .attr("fill", "#6366f1")
    .attr("stroke", "#818cf8")
    .attr("stroke-width", 1.5);

  simulation.on("tick", () => {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  });
}

onMounted(render);
watch(() => [props.nodes, props.links], render, { deep: true });
</script>

<template>
  <div class="card overflow-hidden p-2">
    <svg ref="svgRef" width="600" height="400" class="w-full rounded-lg bg-bg"></svg>
  </div>
</template>
