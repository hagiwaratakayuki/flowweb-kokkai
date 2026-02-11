<script>
  const baseTitle = "Thought Flow 国会編";
  export let title = "";
  let _title = "";
  $: {
    if (!!title == true) {
      _title = title + " - " + baseTitle;
    } else {
      _title = baseTitle;
    }
  }
</script>

<svelte:head>
  <title>{_title}</title>
</svelte:head>
