import { useEffect, useState } from "react";

export default function Home() {
  const [setupData, setSetupData] = useState(); // This is passed in from Dashibase

  async function importClient() {
    const PluginClient = (await import ('@dashibase/plugin-client')).default;
    const client = new PluginClient();

    client.onSetup((data) => {
      console.log(`Received SETUP message ${JSON.stringify(data)}`)
      setSetupData(data);
    })

    client.init();
  }

  useEffect(() => {
    importClient();
  }, []);

  return (
    <div>
      <div>Hello World</div>
      <pre>{ JSON.stringify(setupData, null, 2) }</pre>
    </div>
  )
}