<script>
  let input = "";
  let result = null;
	// For calculating CRC from the first 28 bytes against the received CRC (last 4 bytes)
  function crc16Ccitt(data) {
    let crc = 0xFFFF;

    for (const byte of data) {
      crc ^= byte << 8;

      for (let i = 0; i < 8; i++) {
        if (crc & 0x8000) {
          crc = ((crc << 1) ^ 0x1021) & 0xFFFF;
        } else {
          crc = (crc << 1) & 0xFFFF;
        }
      }
    }

    return crc;
  }

  function decodePacket(hex) {
    // Allow spaces and newlines between hexadecimal bytes.
    const cleaned = hex.trim().replace(/\s+/g, "");
		// If hexadecimal textarea is empty
    if (!cleaned) {
      return { error: "Enter a hexadecimal packet first." };
    }
		// If hexadecimal textarea contains non-hexadecimal characters
    if (!/^[0-9a-fA-F]+$/.test(cleaned)) {
      return { error: "Invalid input: use hexadecimal characters only." };
    }
		// Ensures each byte contains exactly 2 hex digits
    if (cleaned.length % 2 !== 0) {
      return { error: "Each byte must contain exactly two hex digits." };
    }

    const bytes = cleaned.match(/.{2}/g)
      .map((byte) => parseInt(byte, 16));

    // 1 + 4 + 2 + 4 + 17 + 2 + 2 = 32 bytes
    if (bytes.length !== 32) {
      return {
        error: `Expected 32 bytes, but received ${bytes.length} bytes.`
      };
    }

    // Start marker
    const start = bytes[0];

    const startTypes = {
		  0x21: {
		    symbol: "!",
		    description: "No response expected"
		  },
		  0x22: {
		    symbol: '"',
		    description: "Response/Acknowledgment"
		  },
		  0x23: {
		    symbol: "#",
		    description: "Discard message - for human"
		  },
		  0x24: {
		    symbol: "$",
		    description: "Response/Acknowledgment expected"
		  }
		};
		
		const startType = startTypes[start];
		
		if (!startType) {
		  return { error: "Invalid start byte." };
		}

    // Sequence ID: 4-byte unsigned big-endian integer
    const sequenceId = bytes[1] * 0x1000000
      + bytes[2] * 0x10000
      + bytes[3] * 0x100
      + bytes[4];

    // Message ID: 2 ASCII characters
    const messageId = String.fromCharCode(
      bytes[5], bytes[6]
    );

    if (!/^[a-z]{2}$/.test(messageId)) {
      return { error: "Invalid message ID." };
    }

    // Timestamp: 4-byte unsigned big-endian integer
    const timestamp = bytes[7] * 0x1000000
      + bytes[8] * 0x10000
      + bytes[9] * 0x100
      + bytes[10];

    // Payload: 17 bytes
    const payloadBytes = bytes.slice(11, 28);

    const isAscii = payloadBytes.every(
      (byte) => byte >= 0x20 && byte <= 0x7E
    );

    const payloadAscii = isAscii
      ? String.fromCharCode(...payloadBytes)
      : null;

    // Received CRC: 2-byte big-endian integer
    const receivedCrc = (bytes[28] << 8) | bytes[29];

    // Assumption: CRC covers start byte through payload.
    const calculatedCrc = crc16Ccitt(bytes.slice(0, 28));

    // End marker: carriage return + line feed
    const validEnd = bytes[30] === 0x0D
      && bytes[31] === 0x0A;

    return {
      error: null,
      start: `0x${start.toString(16).toUpperCase().padStart(2, "0")}`,
			startSymbol: startType.symbol,
			startDescription: startType.description,
      sequenceId,
      messageId,
      timestamp,
      payloadHex: payloadBytes
        .map((byte) => byte.toString(16).toUpperCase().padStart(2, "0"))
        .join(" "),
      payloadAscii,
      receivedCrc: receivedCrc.toString(16).toUpperCase().padStart(4, "0"),
      calculatedCrc: calculatedCrc.toString(16).toUpperCase().padStart(4, "0"),
      crcValid: receivedCrc === calculatedCrc,
      validEnd
    };
  }

  function handleDecode() {
    result = decodePacket(input);
  }
</script>

<svelte:head>
  <title>Avionics GCS Packet Decoder</title>
  <meta
    name="description"
    content="For Avionics GCS Onboarding"
  />
</svelte:head>

<main>
  <header>
    <h1>Avionics GCS Packet Decoder</h1>
    <p>Paste a hexadecimal packet to inspect its fields.</p>
  </header>

  <section class="panel">
    <label for="packet">Hexadecimal packet</label>

    <textarea
      id="packet"
      bind:value={input}
      placeholder="21 00 00 00 03 62 61 ..."
      rows="4"
      spellcheck="false"
    ></textarea>

    <button onclick={handleDecode}>Decode Packet</button>
  </section>

  {#if result}
    {#if result.error}
      <section class="error">
        <strong>Unable to decode packet</strong>
        <p>{result.error}</p>
      </section>
    {:else}
      <section class="results">
        <h2>Decoded Fields</h2>

        <div class="field">
				  <span>Start Byte</span>
				  <strong>{result.start} ({result.startSymbol}) {result.startDescription}</strong>
				</div>

        <div class="field">
          <span>Sequence ID</span>
          <strong>{String(result.sequenceId).padStart(4, "0")}</strong>
        </div>

        <div class="field">
          <span>Message ID</span>
          <strong>{result.messageId}</strong>
        </div>

        <div class="field">
          <span>Timestamp</span>
          <strong>{result.timestamp} ms</strong>
        </div>

        <div class="field">
          <span>Payload (Hex)</span>
          <strong>{result.payloadHex}</strong>
        </div>

        <div class="field">
          <span>Payload (ASCII)</span>
          <strong>{result.payloadAscii ?? "Not printable ASCII"}</strong>
        </div>

        <div class="field">
          <span>Received CRC</span>
          <strong>{result.receivedCrc}</strong>
        </div>

        <div class="field">
          <span>Calculated CRC</span>
          <strong>{result.calculatedCrc}</strong>
        </div>

        <div class="field">
          <span>CRC Validation</span>
          <strong class:good={result.crcValid}
                  class:bad={!result.crcValid}>
            {result.crcValid ? "Valid" : "Mismatch"}
          </strong>
        </div>

        <div class="field">
          <span>End Marker</span>
          <strong class:good={result.validEnd}
                  class:bad={!result.validEnd}>
            {result.validEnd ? "Valid (CRLF)" : "Invalid"}
          </strong>
        </div>
      </section>
    {/if}
  {/if}
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: #f4f6f8;
    color: #1f2937;
  }

  main {
    max-width: 800px;
    margin: 40px auto;
    padding: 24px;
  }

  header {
    margin-bottom: 24px;
  }

  h1 {
    margin-bottom: 8px;
  }

  header p {
    color: #64748b;
  }

  .panel, .results, .error {
    background: white;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px #0000000a;
  }

  label {
    display: block;
    font-weight: 600;
    margin-bottom: 10px;
  }

  textarea {
    box-sizing: border-box;
    width: 100%;
    padding: 12px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font: 14px monospace;
    resize: vertical;
  }

  button {
    margin-top: 14px;
    padding: 12px 18px;
    border: none;
    border-radius: 8px;
    background: #2563eb;
    color: white;
    font-weight: 600;
    cursor: pointer;
  }

  button:hover {
    background: #1d4ed8;
  }

  h2 {
    margin-top: 0;
  }

  .field {
    display: grid;
    grid-template-columns: 180px minmax(0, 1fr);
    gap: 12px;
    padding: 14px 0;
    border-bottom: 1px solid #e5e7eb;
  }

  .field span {
    color: #64748b;
  }

  .field strong {
    overflow-wrap: anywhere;
  }

  .good {
    color: #15803d;
  }

  .bad {
    color: #dc2626;
  }

  .error {
    color: #b91c1c;
  }

  @media (max-width: 550px) {
    main {
      margin: 10px auto;
      padding: 14px;
    }

    .field {
      grid-template-columns: 1fr;
      gap: 6px;
    }
  }
</style>
