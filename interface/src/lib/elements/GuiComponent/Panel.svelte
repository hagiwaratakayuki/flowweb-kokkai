<script>
  let className = "";
  export { className as class };
</script>

<div class={"bg-white mb-3 p-2 rounded " + className}>
  <slot></slot>
</div>
