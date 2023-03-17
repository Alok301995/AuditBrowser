// JS FOR CHARTS





 export async function build_chart(data) {
    await new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.map((row) => row.attribute),
        datasets: [
          {
            label: "Amount of bits of info",
            data: data.map((row) => row.bits_of_info),
          },
        ],
      },
    });
  };
  