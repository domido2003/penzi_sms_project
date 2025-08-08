import React from "react";

function Footer() {
  return (
    <div style={styles.footer}>
      <span style={styles.text}>Powered by</span>
      <img
        src="/onfon.jpeg"
        alt="Onfon Logo"
        style={styles.logo}
      />
    </div>
  );
}

const styles = {
  footer: {
    padding: "12px 24px",
    backgroundColor: "#c2185b", // deep rose
    color: "#fff",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    borderTop: "1px solid #b21655",
    gap: "8px",
  },
  text: {
    fontSize: "14px",
    fontWeight: "500",
  },
  logo: {
    height: "22px",
    objectFit: "contain",
    // Removed filter
  },
};

export default Footer;
