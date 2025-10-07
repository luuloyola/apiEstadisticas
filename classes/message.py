class Message:
  def __init__(self, rows: []):
    self.id = rows[0]
    self.chat_id = rows[1]
    self.content = rows[2]
    self.created_at = rows[3]
    self.sentiment = None


  def get_id(self):
      return self.id

  def get_content(self):
      return self.content

  def get_chat_id(self):
      return self.chat_id

  def get_sentiment(self):
      return self.sentiment

  def get_created_at(self):
      return self.created_at

  def set_sentiment(self, sentiment):
      self.sentiment = sentiment

  def __str__(self):
      return (
          f"💬 Mensaje (ID: {self.id})\n"
          f"- Chat ID: {self.chat_id}\n"
          f"- Contenido: {self.content[:100]}{'...' if len(self.content) > 100 else ''}\n"
          f"- Creado en: {self.created_at}\n"
          f"- Sentimiento: {self.sentiment if self.sentiment else 'No asignado'}"
      )