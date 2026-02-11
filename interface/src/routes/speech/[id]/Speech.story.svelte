<script>
  import Speech from "./+page.svelte";
  import ComponentLayout from "$lib/elements/ComponentLayout.svelte";
  /**
   * @type {import("histoire").StoryFile}
   */
  export let Hst;

  /**
   * @type {import("$lib/ml_api/api_types/SpeechOverview").SpeechOverview[]}
   */
  const discussion = [
    {
      id: "test",
      title: "本日はお日柄も良く",
      meeting: "テスト委員会",
      speaker: "サンプルさん",
    },
    {
      id: "test2",
      title: "大変良い日和で",
      meeting: "テスト委員会",
      speaker: "テストさん",
    },
  ];
  /** @type {import('./$types').PageData} */
  const data = {
    speech: {
      id: "test2",
      body: "大変良い日和ですが、残念ながら仏滅です",
      speaker: "テストさん",
      meeting: "テスト委員会",
      house: "参議院",
      session: "201",
      issue: "第一号",
      url: "http://test.example.com",
    },
    discussion,
    clusters: [],
  };
</script>

<Hst.Story>
  <ComponentLayout>
    <Speech {data} />
  </ComponentLayout>
</Hst.Story>
