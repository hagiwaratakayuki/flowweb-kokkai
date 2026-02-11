<script>
  import {
    CardBody,
    Card,
    CardHeader,
    CardTitle,
  } from "@sveltestrap/sveltestrap";
  import { getDate } from "$lib/util/get_date";
  /**
   * @type {import("$lib/ml_api/api_types/TextOverview").TextOverview}
   */
  export let overview = undefined;
</script>

<Card>
  <CardHeader class="bg-secondary">
    <CardTitle>
      <a href="/text/{overview.id}" class="text-white">
        {overview.title}
      </a>
    </CardTitle>
  </CardHeader>
  <CardBody>
    <p><b class="me-1">Author:</b>{overview.author}</p>
    <p><b class="me-1">published</b>{getDate(overview.published)}</p>
    <p class="text-center"><a href="/text/{overview.id}">more</a></p>
  </CardBody>
</Card>
